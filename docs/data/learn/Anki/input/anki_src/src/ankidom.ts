import { breakOnSlashes, combineWithSlashes } from "./parse_helpers";

export type ANSWER_CALLBACK = (postMortem: 0 | 1 | 2| 3 | 4 | 5) => Promise<void>;

export class AnkiDom {
    private readonly questionTags: HTMLUListElement[];
    private originalQuestionTag: HTMLUListElement | null = null;
    private processedQuestionTag: HTMLUListElement | null = null;
    private infoQuestionCount: number | undefined = undefined;
    private infoOutOfQuestionsFlag: boolean | undefined = undefined;

    constructor() {
        this.questionTags = AnkiDom.findQuestionTags();
        this.hideAllQuestionTags();
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

        const answerPatterns = AnkiDom.findAndRemovePatternTags(this.processedQuestionTag, 'anki-answerpattern');
        for (const [patternIdx, pattern] of answerPatterns.entries()) {
            AnkiDom.blackoutPattern(this.processedQuestionTag, pattern, '' + patternIdx);
        }
        
        const hidePatterns = AnkiDom.findAndRemovePatternTags(this.processedQuestionTag, 'anki-hidepattern');
        for (const pattern of hidePatterns) {
            AnkiDom.blackoutPattern(this.processedQuestionTag, pattern, 'HIDDEN', 'black');
        }

        AnkiDom.addClozeWordAnswerZone(this.processedQuestionTag, answerPatterns, callback);

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
        const nodeIt = document.evaluate(".//span[@class=\"anki-deadquestion\"]", this.questionTags[id], null, XPathResult.ANY_TYPE, null);
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
        const nodeIt = document.evaluate(".//span[@class=\"anki-infopanel\"]", document, null, XPathResult.ANY_TYPE, null);
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

    private static findAndRemovePatternTags(parent: HTMLElement, classAttr: string): RegExp[] {
        const nodeIt = document.evaluate(".//span[@class=\"" + classAttr + "\"]", parent, null, XPathResult.ANY_TYPE, null);
        const ret: RegExp[] = []
        let node = nodeIt.iterateNext();
        while (node !== null) {
            node.parentElement?.removeChild(node);
            if (!(node instanceof Element)) {
                continue;
            }
            const txt = node.getAttribute("data-pattern"); // Why use an attr instead of textContent? markdown-it applies escaping to stuff inside tag before it spits it out, which may produce invalid regex.
            if (txt === null) {
                throw new Error(`Word pattern expects data-pattern attribute.\n\n${node.innerHTML}`);
            }
            const info = (() => {
                const broken = breakOnSlashes(txt);
                switch(broken.length) {
                    case 1:
                        return {
                            regex: '(' + broken[0] + ')',
                            flags: 'i'
                        };
                    case 2:
                        return {
                            regex: broken[0],
                            flags: broken[1]
                        };
                    default:
                        throw new Error(
                            'Incorrect number of arguments in guess_word tag: ' + JSON.stringify(broken) + '\n'
                            + '------\n'
                            + 'Examples:\n'
                            + '  my bookmark\n'
                            + '  (my\\s+bookmark)/i\n'
                            + 'Tag arguments are delimited using forward slash (\\). Use \\ to escape the delimiter (\\/).'
                        );
                }
            })();
            ret.push(
                new RegExp(info.regex, info.flags)
            );
            node = nodeIt.iterateNext();
        }
        return ret;
    }

    private static blackoutPattern(parent: HTMLElement, pattern: RegExp, blackoutText: string, blackoutColor?: string) {
        function hide(node: Node) {
            if (node.nodeName === '#text') {
                const text = (node as CharacterData).data;
                const regex = RegExp(pattern.source, pattern.flags + 'g'); // g required
                const containerNode = document.createElement('span');
                let regexFoundCount = 0;
                let regexLastFoundIdx = 0;
                let found;
                while ((found = regex.exec(text)) !== null) {
                    if (found[0].trim().length === 0) {
                        throw new Error(`Regex pattern is matching 0 length substring: regex ${pattern.source} found at index ${found.index} of text ${text}\n\n${parent.textContent}`);
                    }
                    const preTextNode = document.createTextNode(
                        text.slice(regexLastFoundIdx, found.index)
                    );
                    const replacementNode = AnkiDom.createBlackoutPatternLabel(blackoutText, blackoutColor);
                    containerNode.appendChild(preTextNode);
                    containerNode.appendChild(replacementNode);
                    regexLastFoundIdx = regex.lastIndex;
                    regexFoundCount += 1;
                }
                const finalTextNode = document.createTextNode(
                    text.slice(regexLastFoundIdx)
                );
                containerNode.appendChild(finalTextNode);
                if (node.parentNode === null) {
                    throw new Error('Null parent');
                }
                if (regexFoundCount > 0) { // only apply change if something was found
                    node.parentNode.replaceChild(containerNode, node);
                }
            }
            for (let childNode of (node as Element).childNodes) {
                hide(childNode)
            }
        }
        hide(parent);
    }

    private static createBlackoutPatternLabel(text: string, color?: string) {
        const labelNode = document.createElement('span');
        labelNode.appendChild(
            document.createTextNode(
                '{' + text + '}'
            )
        );
        const hash = Math.abs(text.split('').reduce((prevHash, currVal) => (((prevHash << 5) - prevHash) + currVal.charCodeAt(0))|0, 0)); // https://stackoverflow.com/a/34842797
        // hiddenNode.style.visibility = 'hidden;
        labelNode.style.color = 'white';
        labelNode.style.backgroundColor =  color || `hsl(${hash * 137.508},50%,75%)`; // https://stackoverflow.com/a/20129594
        labelNode.style.fontWeight = 'bold';
        labelNode.style.userSelect = 'none';
        return labelNode;
    }

    private static addClozeWordAnswerZone(parent: HTMLElement, patterns: RegExp[], callback: ANSWER_CALLBACK) {
        const divElem = document.createElement('div');
        const answerTextElems: HTMLInputElement[] = [];
        for (const [patternIdx, pattern] of patterns.entries()) {
            const answerTextElem = document.createElement('input');
            answerTextElem.type = 'text';
            answerTextElem.autocomplete = 'off';
            answerTextElem.id = combineWithSlashes([pattern.source, pattern.flags]);
            const labelNode = AnkiDom.createBlackoutPatternLabel('' + patternIdx);
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
            for (let i = 0; i < answerTextElems.length; i++) {
                const pattern = patterns[i];
                const answerTextElem = answerTextElems[i];
                const answer = answerTextElem.value;
                const match = answer.match(pattern);
                if (match === null || match[0].length !== answer.length){
                    questionPassed = false;
                    break;
                }
            }
            submitButtonElem.disabled = true;
            this.addClozeWordPostMortemZone(parent, questionPassed, patterns, callback);
        };
        divElem.appendChild(submitButtonElem);
        divElem.style.borderWidth = '1px';
        divElem.style.borderStyle = 'solid';
        parent.appendChild(divElem);
    }

    private static addClozeWordPostMortemZone(parent: HTMLElement, correctAnswer: boolean, patterns: RegExp[], callback: ANSWER_CALLBACK) {
        const divElem = document.createElement('div');
        const labelElem = document.createElement('p');
        labelElem.appendChild(
            document.createTextNode(`Answer was ${correctAnswer ? 'correct' : 'incorrect'}!`)
        )
        labelElem.style.backgroundColor = correctAnswer ? 'green' : 'red';
        divElem.appendChild(labelElem);
        const answerTextElem = document.createElement('p');
        for (const [patternIdx, pattern] of patterns.entries()) {
            const labelNode = AnkiDom.createBlackoutPatternLabel('' + patternIdx);
            answerTextElem.appendChild(labelNode);
            answerTextElem.appendChild(
                document.createTextNode(
                    ' = ' + combineWithSlashes([pattern.source, pattern.flags])
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
            for (const [ label, grade ] of items) {
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
            for (const [ label, grade ] of items) {
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