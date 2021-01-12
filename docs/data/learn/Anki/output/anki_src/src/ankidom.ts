import { Entry, Key, RegexScannerCollection, ScannerEntry } from "./regex_scanner_collection";
import { breakOnSlashes, combineWithSlashes } from "./utils/parse_helpers";

export type ANSWER_CALLBACK = (postMortem: 0 | 1 | 2 | 3 | 4 | 5) => Promise<void>;

const ANSWER_PATTERN_CLASS = 'anki-answerpattern';
const HIDE_PATTERN_CLASS = 'anki-hidepattern';
const IGNORE_PATTERN_CLASS = 'anki-ignorepattern';
const RANDOM_ORDER_LIST_CLASS = 'anki-randomorderlist';
const DEAD_QUESTION_CLASS = 'anki-deadquestion';
const INFO_PANEL_CLASS = 'anki-infopanel';
const DEBUG_FORCE_SHOW_CLASS = 'anki-debugforceshow';

class IgnorePattern {
    public constructor() { }
}

class HidePattern {
    public constructor() { }
}

class AnswerPattern {
    public readonly bgColor: string;
    public readonly fgColor: string;
    public readonly label: string;

    public constructor(
        public readonly answerOrder: number
    ) {
        this.label = '' + answerOrder;
        const labelHash = Math.abs(this.label.split('').reduce((prevHash, currVal) => (((prevHash << 5) - prevHash) + currVal.charCodeAt(0)) | 0, 0)); // https://stackoverflow.com/a/34842797
        this.bgColor = `hsl(${labelHash * 137.508},50%,75%)`; // https://stackoverflow.com/a/20129594
        this.fgColor = 'white';
    }
}

export class AnkiDom {
    private readonly questionTags: HTMLUListElement[];
    private originalQuestionTag: HTMLUListElement | null = null;
    private processedQuestionTag: HTMLUListElement | null = null;
    private infoQuestionCount: number | undefined = undefined;
    private infoOutOfQuestionsFlag: boolean | undefined = undefined;

    constructor() {
        this.questionTags = AnkiDom.findQuestionTags();
        this.hideAllQuestionTags();
        for (const questionTag of this.questionTags) {
            AnkiDom.findPatternTags(questionTag, [IGNORE_PATTERN_CLASS, HIDE_PATTERN_CLASS, ANSWER_PATTERN_CLASS], false);  // validate regexes
            if (AnkiDom.findDebugForceShowTag(questionTag)) {
                this.questionTags = [questionTag];
                break;
            }
        }
    }

    private static findQuestionTags(): HTMLUListElement[] {
        const liNodeIt = document.evaluate("//ul[not(ancestor::ul)][1]/li", document, null, XPathResult.ANY_TYPE, null);
        const ret: HTMLUListElement[] = []
        let liNode = liNodeIt.iterateNext();
        while (liNode !== null) {
            ret.push(liNode as HTMLUListElement);
            liNode = liNodeIt.iterateNext();
        }
        return ret;
    }

    private hideAllQuestionTags() {
        for (const bullet of this.questionTags) {
            bullet.style.display = 'none';
        }
    }

    public getQuestionCount(): number {
        return this.questionTags.length;
    }

    public showQuestion(id: number, callback: ANSWER_CALLBACK) {
        if (this.processedQuestionTag !== null && this.originalQuestionTag !== null) {
            AnkiDom.swapElement(
                this.processedQuestionTag,
                this.originalQuestionTag
            );
        }
        this.originalQuestionTag = this.questionTags[id];
        this.processedQuestionTag = this.originalQuestionTag.cloneNode(true) as HTMLUListElement;

        // Reorder any lists that are marked to be reordered
        AnkiDom.findAndProcessReorderListTags(this.processedQuestionTag);

        // Pull out all regex patterns
        const allPatterns = AnkiDom.findPatternTags(this.processedQuestionTag, [IGNORE_PATTERN_CLASS, HIDE_PATTERN_CLASS, ANSWER_PATTERN_CLASS], true);
        const scanner = new RegexScannerCollection();

        // Pull out ignore regexes.
        const ignorePatterns = allPatterns.filter(p => p.class === IGNORE_PATTERN_CLASS);
        for (const pattern of ignorePatterns) {
            scanner.addBookmark(
                new Key(pattern.regex, pattern.flags),
                pattern.showPreamble,
                pattern.showPostamble,
                new IgnorePattern()
            );
        }

        // Pull out answer regexes. The order is important because the regexes may match overlapping text and the user-defined order
        // is the order in which matching should occur. However, the answer regexes also need to be DISPLAYED to the user in a
        // randomized order because the user may end up memorizing that "when I see this question answer A goes in slot 1, answer B
        // goes in slow 2, etc.." instead of memorizing the actual content.
        const answerPatterns = allPatterns.filter(p => p.class === ANSWER_PATTERN_CLASS);
        const answerPatternKeys = [...answerPatterns.keys()];
        AnkiDom.shuffleArray(answerPatternKeys);
        const answerPatternsOrderedByKeys = Array(answerPatterns.length);
        for (const [patternIdx, pattern] of answerPatterns.entries()) { // black out in user defined order, but display with shuffled keys
            const remappedKey = answerPatternKeys[patternIdx];
            answerPatternsOrderedByKeys[remappedKey] = pattern;
            scanner.addBookmark(
                new Key(pattern.regex, pattern.flags),
                pattern.showPreamble,
                pattern.showPostamble,
                new AnswerPattern(remappedKey)
            );
        }

        // Pull out hide regexes.
        const hidePatterns = allPatterns.filter(p => p.class === HIDE_PATTERN_CLASS);
        for (const pattern of hidePatterns) {
            scanner.addBookmark(
                new Key(pattern.regex, pattern.flags),
                pattern.showPreamble,
                pattern.showPostamble,
                new HidePattern()
            );
        }

        // Black out regexes
        AnkiDom.blackoutPattern(this.processedQuestionTag, scanner);

        // Add answer zone.
        AnkiDom.addClozeWordAnswerZone(this.processedQuestionTag, scanner, callback);

        this.processedQuestionTag.style.display = 'block';

        AnkiDom.swapElement(
            this.originalQuestionTag,
            this.processedQuestionTag
        );
    }

    public hideQuestion(id: number) {
        if (this.processedQuestionTag !== null && this.originalQuestionTag !== null) {
            AnkiDom.swapElement(
                this.processedQuestionTag,
                this.originalQuestionTag
            );
        }
        this.originalQuestionTag = null;
        this.processedQuestionTag = null;

        this.questionTags[id].style.display = 'none';
    }

    public isDeadQuestion(id: number) {
        const nodeIt = document.evaluate(`.//span[@class="${DEAD_QUESTION_CLASS}"]`, this.questionTags[id], null, XPathResult.ANY_TYPE, null);
        const node = nodeIt.iterateNext();
        return node !== null;
    }

    public setQuestionCount(questionCount: number) {
        this.infoQuestionCount = questionCount;
        this.findAndUpdateInfoTag();
    }

    public setOutOfQuestionsFlag(outOfQuestions: boolean) {
        this.infoOutOfQuestionsFlag = outOfQuestions;
        this.findAndUpdateInfoTag();
    }

    private findAndUpdateInfoTag() {
        const nodeIt = document.evaluate(`.//span[@class="${INFO_PANEL_CLASS}"]`, document, null, XPathResult.ANY_TYPE, null);
        const node = nodeIt.iterateNext();
        while (node === null) {
            console.error('info node not found');
            return;
        }
        const children = Array(...node.childNodes.values());
        children.forEach(c => node.removeChild(c));
        let t: string[] = [];
        if (this.infoOutOfQuestionsFlag === true) {
            t.push(`No more questions`);
        }
        if (this.infoQuestionCount !== undefined) {
            t.push(`Total questions: ${this.infoQuestionCount}`);
        }
        node.appendChild(
            document.createTextNode(
                t.join(' / ')
            )
        );
    }

    private static findDebugForceShowTag(parent: HTMLElement): boolean {
        const nodeIt = document.evaluate(".//span[@class=\"" + DEBUG_FORCE_SHOW_CLASS + "\"]", parent, null, XPathResult.ANY_TYPE, null);
        return nodeIt.iterateNext() !== null;
    }

    private static findPatternTags(parent: HTMLElement, classAttrs: string[], removeTag: boolean) {
        const nodeIt = document.evaluate(".//span[" + classAttrs.map(c => `@class="${c}"`).join(" or ") + "]", parent, null, XPathResult.ANY_TYPE, null);
        const nodes = AnkiDom.xPathResultToArray(nodeIt); // place results in array to because modding while iterating causes some browsers to barf
        const classAttrsSet = new Set(classAttrs);
        const ret = []
        for (const node of nodes) {
            if (removeTag) {
                node.parentElement?.removeChild(node);
            }
            if (!(node instanceof Element)) {
                continue;
            }
            const txt = node.getAttribute("data-pattern"); // Why use an attr instead of textContent? markdown-it applies escaping to stuff inside tag before it spits it out, which may produce invalid regex.
            if (txt === null) {
                throw new Error(`Word pattern expects data-pattern attribute.\n\n${node.innerHTML}`);
            }
            const nodeClasses = new Array(...node.classList);
            const relevantNodeClasses = nodeClasses.filter(c => classAttrsSet.has(c));
            if (relevantNodeClasses.length !== 1) {
                throw new Error(`Unexpected classes ${nodeClasses} vs ${classAttrs}`);
            }
            const info = (() => {
                const broken = breakOnSlashes(txt);
                switch (broken.length) {
                    case 1:
                        return {
                            regex: '(' + broken[0] + ')',
                            flags: 'i',
                            showPreamble: false,
                            showPostamble: false,
                            class: relevantNodeClasses[0]
                        };
                    case 2:
                        return {
                            regex: broken[0],
                            flags: broken[1],
                            showPreamble: false,
                            showPostamble: false,
                            class: relevantNodeClasses[0]
                        };
                    case 4:
                        return {
                            regex: broken[0],
                            flags: broken[1],
                            showPreamble: AnkiDom.toBoolean(broken[2]),
                            showPostamble: AnkiDom.toBoolean(broken[3]),
                            class: relevantNodeClasses[0]
                        }
                    default:
                        throw new Error(
                            'Incorrect number of arguments in ' + relevantNodeClasses[0] + ' tag: ' + JSON.stringify(broken) + '\n'
                            + '------\n'
                            + 'Examples:\n'
                            + '  `bookmark\\s+regex`\n'
                            + '  `(bookmark\\s+regex)/i`\n'
                            + '  `(bookmark\\s+regex)/i/true/true`\n'
                            + 'Tag arguments are delimited using forward slash (\\). Use \\ to escape the delimiter (\\/).'
                        );
                }
            })();
            ret.push(info);
        }
        return ret;
    }

    private static toBoolean(s: string) {
        switch (s) {
            case 'true': return true;
            case 'false': return false;
            default: throw new Error(s + ' cannot be converted to boolean');
        }
    }

    private static findAndProcessReorderListTags(parent: HTMLElement) {
        const nodeIt = document.evaluate(".//span[@class=\"" + RANDOM_ORDER_LIST_CLASS + "\"]/ancestor::ul[1]|.//span[@class=\"" + RANDOM_ORDER_LIST_CLASS + "\"]/ancestor::ol[1]", parent, null, XPathResult.ANY_TYPE, null);
        const nodes = AnkiDom.xPathResultToArray(nodeIt); // place results in array to because modding while iterating causes some browsers to barf
        for (const node of nodes) {
            if (!(node instanceof Element)) {
                continue;
            }
            const children = Array(...node.childNodes);
            for (const child of children) {
                child.parentElement?.removeChild(child);
            }
            AnkiDom.shuffleArray(children);
            for (const child of children) {
                node.insertBefore(child, null);
            }
        }
    }

    private static xPathResultToArray(res: XPathResult): Node[] {
        const nodes = [];
        let node = res.iterateNext();
        while (node !== null) {
            nodes.push(node);
            node = res.iterateNext();
        }
        return nodes;
    }

    // https://stackoverflow.com/a/12646864
    private static shuffleArray(array: any[]) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    private static blackoutPattern(parent: HTMLElement, scanner: RegexScannerCollection) {
        function hide(node: Node) {
            if (node.nodeName === '#text') {
                const containerNode = document.createElement('span');
                let content = (node as CharacterData).data
                let regexFoundCount = 0;
                while (true) {
                    const scanResult = scanner.scan(content);
                    if (scanResult === null) {
                        const finalTextNode = document.createTextNode(content);
                        containerNode.appendChild(finalTextNode);
                        break;
                    }

                    const startMatchIdx = scanResult.fullIndex;
                    const endMatchIdx = scanResult.fullIndex + scanResult.fullMatch.length;

                    const preText = content.substring(0, startMatchIdx);
                    const capturePreambleText = scanResult.capturePreamble;
                    const captureText = scanResult.captureMatch;
                    const capturePostambleText = scanResult.capturePostamble;
                    const postText = content.substring(endMatchIdx);

                    // pre
                    containerNode.appendChild(
                        document.createTextNode(preText)
                    );
                    if (capturePreambleText !== null) {
                        containerNode.appendChild(
                            document.createTextNode(capturePreambleText)
                        )
                    }
                    // content
                    if (scanResult.extraData instanceof HidePattern) {
                        containerNode.appendChild(
                            AnkiDom.createBlackoutPatternLabel('HIDDEN', 'black', 'white')
                        );
                    } else if (scanResult.extraData instanceof AnswerPattern) {
                        containerNode.appendChild(
                            AnkiDom.createBlackoutPatternLabel(scanResult.extraData.label, scanResult.extraData.bgColor, scanResult.extraData.fgColor)
                        );
                    } else if (scanResult.extraData instanceof IgnorePattern) {
                        containerNode.appendChild(
                            document.createTextNode(captureText)
                        );
                    }
                    // post
                    if (capturePostambleText !== null) {
                        containerNode.appendChild(
                            document.createTextNode(capturePostambleText)
                        )
                    }

                    content = postText;
                    regexFoundCount += 1;
                }
                if (regexFoundCount > 0) { // only apply change if something was found
                    if (node.parentNode === null) {
                        throw new Error('Null parent');
                    }
                    node.parentNode.replaceChild(containerNode, node);
                }
            }

            for (let childNode of (node as Element).childNodes) {
                hide(childNode);
            }
        }
        hide(parent);
    }

    private static createBlackoutPatternLabel(text: string, bgColor: string | null, fgColor: string | null) {
        const labelNode = document.createElement('span');
        labelNode.appendChild(
            document.createTextNode(
                '{' + text + '}'
            )
        );
        // hiddenNode.style.visibility = 'hidden;
        if (fgColor !== null) {
            labelNode.style.color = fgColor;
        }
        if (bgColor !== null) {
            labelNode.style.backgroundColor = bgColor;
        }
        labelNode.style.fontWeight = 'bold';
        labelNode.style.userSelect = 'none';
        return labelNode;
    }

    private static addClozeWordAnswerZone(parent: HTMLElement, scanner: RegexScannerCollection, callback: ANSWER_CALLBACK) {
        const divElem = document.createElement('div');
        const answerTextElems: HTMLInputElement[] = [];
        const orderedEntries = Array(...scanner.viewEntries())
            .filter(e => e.entry.extraData instanceof AnswerPattern)
            .map(e => [e, e.entry.extraData as AnswerPattern] as [ScannerEntry, AnswerPattern])
            .sort((a, b) => a[1].answerOrder - b[1].answerOrder);
        for (const [entry, answerPattern] of orderedEntries) {
            const answerTextElem = document.createElement('input');
            answerTextElem.type = 'text';
            answerTextElem.autocomplete = 'off';
            answerTextElem.autocapitalize = 'off';
            answerTextElem.spellcheck = false;
            answerTextElem.id = combineWithSlashes([entry.entry.origKey.regex, entry.entry.origKey.flags]);
            const labelNode = AnkiDom.createBlackoutPatternLabel(answerPattern.label, answerPattern.bgColor, answerPattern.fgColor);
            divElem.appendChild(labelNode);
            divElem.appendChild(answerTextElem);
            divElem.appendChild(
                document.createElement('p')
            );
            answerTextElems.push(answerTextElem);
        }
        const submitButtonElem = document.createElement('button');
        submitButtonElem.appendChild(
            document.createTextNode('Answer')
        );
        submitButtonElem.onclick = (e) => {
            let questionPassed = true;
            for (let i = 0; i < orderedEntries.length; i++) {
                const [pattern, _] = orderedEntries[i];
                const answerTextElem = answerTextElems[i];
                const answer = answerTextElem.value;
                const match = pattern.scanner.scan(answer);
                if (match === null || match.captureMatch !== answer) {
                    questionPassed = false;
                    break;
                }
            }
            submitButtonElem.disabled = true;
            this.addClozeWordPostMortemZone(parent, questionPassed, scanner, callback);
        };
        divElem.appendChild(submitButtonElem);
        divElem.style.borderWidth = '1px';
        divElem.style.borderStyle = 'solid';
        parent.appendChild(divElem);
    }

    private static addClozeWordPostMortemZone(parent: HTMLElement, correctAnswer: boolean, scanner: RegexScannerCollection, callback: ANSWER_CALLBACK) {
        const divElem = document.createElement('div');
        const labelElem = document.createElement('p');
        labelElem.appendChild(
            document.createTextNode(`Answer was ${correctAnswer ? 'correct' : 'incorrect'}!`)
        )
        labelElem.style.backgroundColor = correctAnswer ? 'green' : 'red';
        divElem.appendChild(labelElem);
        const answerTextElem = document.createElement('p');
        const orderedEntries = Array(...scanner.viewEntries())
            .filter(e => e.entry.extraData instanceof AnswerPattern)
            .map(e => [e, e.entry.extraData as AnswerPattern] as [ScannerEntry, AnswerPattern])
            .sort((a, b) => a[1].answerOrder - b[1].answerOrder);
        for (const [entry, answerPattern] of orderedEntries) {
            const labelNode = AnkiDom.createBlackoutPatternLabel(answerPattern.label, answerPattern.bgColor, answerPattern.fgColor);
            answerTextElem.appendChild(labelNode);
            answerTextElem.appendChild(
                document.createTextNode(
                    ' = ' + combineWithSlashes([entry.entry.origKey.regex, entry.entry.origKey.flags])
                )
            );
            answerTextElem.appendChild(
                document.createElement('br')
            );
        }
        divElem.appendChild(answerTextElem);
        if (correctAnswer === true) {
            const items: [string, number][] = [
                ['Got answer easily', 5],
                ['Got answer with some hesitation', 4],
                ['Got answer but with difficulty', 3]
            ];
            for (const [label, grade] of items) {
                const buttonElem = document.createElement('button');
                buttonElem.appendChild(
                    document.createTextNode(label)
                );
                buttonElem.onclick = (e) => callback(grade as 0 | 1 | 2 | 3 | 4 | 5);
                divElem.appendChild(buttonElem);
                divElem.appendChild(
                    document.createElement('p')
                );
            }
        } else {
            const items: [string, number][] = [
                ['Recalled after seeing answer with ease', 2],
                ['Recalled after seeing answer but was difficult', 1],
                ['Not recalled after seeing answer', 0]
            ];
            for (const [label, grade] of items) {
                const buttonElem = document.createElement('button');
                buttonElem.appendChild(
                    document.createTextNode(label)
                );
                buttonElem.onclick = (e) => callback(grade as 0 | 1 | 2 | 3 | 4 | 5);
                divElem.appendChild(buttonElem);
                divElem.appendChild(
                    document.createElement('p')
                );
            }
        }
        divElem.style.borderWidth = '1px';
        divElem.style.borderStyle = 'solid';
        parent.appendChild(divElem);
    }

    private static swapElement(originalElement: HTMLElement, replacementElement: HTMLElement) {
        if (originalElement.parentNode === null) {
            throw new Error('Null parent');
        }
        originalElement.parentNode.replaceChild(replacementElement, originalElement);
    }
}