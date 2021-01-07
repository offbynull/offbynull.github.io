import { breakOnSlashes, combineWithSlashes } from "./parse_helpers";

export class AnkiDom {
    private readonly questionTags: HTMLUListElement[];
    private originalQuestionTag: HTMLUListElement | null = null;
    private processedQuestionTag: HTMLUListElement | null = null;

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

        const patterns = AnkiDom.findAndRemovePatternTags(this.processedQuestionTag);
        for (const [patternIdx, pattern] of patterns.entries()) {
            AnkiDom.blackoutClozeWord(this.processedQuestionTag, pattern, patternIdx);
        }
        AnkiDom.addClozeWordAnswerZone(this.processedQuestionTag, patterns, callback);

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
        const nodeIt = document.evaluate(".//dead", this.questionTags[id], null, XPathResult.ANY_TYPE, null);
        const node = nodeIt.iterateNext();
        return node !== null;
    }

    public findAndUpdateInfoTag(passed: 'NONE' | 'PASS' | 'FAIL', questionCount: number) {
        const nodeIt = document.evaluate(".//info", document, null, XPathResult.ANY_TYPE, null);
        const node = nodeIt.iterateNext();
        while (node === null) {
            console.error('info node not found');
            return;
        }
        const children = Array(... node.childNodes.values());
        children.forEach(c => node.removeChild(c));
        node.appendChild(
            document.createTextNode(
                `Last answer: ${passed} / Total questions: ${questionCount}`
            )
        );
    }

    private static findAndRemovePatternTags(parent: HTMLElement): RegExp[] {
        const nodeIt = document.evaluate(".//pattern", parent, null, XPathResult.ANY_TYPE, null);
        const ret: RegExp[] = []
        let node = nodeIt.iterateNext();
        while (node !== null) {
            node.parentElement?.removeChild(node);
            if (node.textContent === null) {
                continue;
            }
            const txt = node.textContent;
            const info = (() => {
                const broken = breakOnSlashes(txt);
                switch(broken.length) {
                    case 1:
                        return {
                            label: broken[0],
                            regex: '(' + broken[0] + ')',
                            flags: 'i'
                        };
                    case 2:
                        return {
                            regex: broken[1],
                            flags: broken[2]
                        };
                    default:
                        throw new Error(
                            'Incorrect number of arguments in guess_word tag: ' + JSON.stringify(broken) + '\n'
                            + '------\n'
                            + 'Examples:\n'
                            + '  `my bookmark`\n'
                            + '  `(my\\s+bookmark)/i`\n'
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

    private static blackoutClozeWord(parent: HTMLElement, pattern: RegExp, patternIdx: number) {
        function hide(node: Node) {
            if (node.nodeName === '#text') {
                const text = (node as CharacterData).data;
                const regex = RegExp(pattern.source, pattern.flags + 'g'); // g required
                const containerNode = document.createElement('span');
                let regexLastFoundIdx = 0;
                let found;
                while ((found = regex.exec(text)) !== null) {
                    const textNode = document.createTextNode(
                        text.slice(regexLastFoundIdx, found.index)
                    );
                    const hiddenNode = document.createElement('span');
                    hiddenNode.appendChild(
                        document.createTextNode(
                            '{' + patternIdx + '}'
                        )
                    );
                    // hiddenNode.style.visibility = 'hidden;
                    hiddenNode.style.color = 'white';
                    hiddenNode.style.backgroundColor = 'red';
                    hiddenNode.style.fontWeight = 'bold';
                    hiddenNode.style.userSelect = 'none';
                    containerNode.appendChild(textNode);
                    containerNode.appendChild(hiddenNode);
                    regexLastFoundIdx = regex.lastIndex;
                }
                const finalTextNode = document.createTextNode(
                    text.slice(regexLastFoundIdx)
                );
                containerNode.appendChild(finalTextNode);
                if (node.parentNode === null) {
                    throw new Error('Null parent');
                }
                node.parentNode.replaceChild(containerNode, node)
            }
            for (let childNode of (node as Element).childNodes) {
                hide(childNode)
            }
        }
        hide(parent);
    }

    private static addClozeWordAnswerZone(parent: HTMLElement, patterns: RegExp[], callback: ANSWER_CALLBACK) {
        const divElem = document.createElement('div');
        const answerTextElems: HTMLInputElement[] = [];
        for (const [patternIdx, pattern] of patterns.entries()) {
            const answerTextElem = document.createElement('input');
            answerTextElem.setAttribute('type', 'text');
            answerTextElem.setAttribute('id', combineWithSlashes([pattern.source, pattern.flags]));
            divElem.appendChild(
                document.createTextNode(`{${patternIdx}}: `)
            );
            divElem.appendChild(answerTextElem);
            divElem.appendChild(
                document.createElement('p')
            );
            answerTextElems.push(answerTextElem);
        }
        const questionShowTime = new Date();
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
            callback(questionPassed, questionShowTime);
        };
        divElem.appendChild(submitButtonElem);
        divElem.style.borderWidth = '1px';
        parent.appendChild(divElem);
    }

    private static swapElement(originalElement: HTMLElement, replacementElement: HTMLElement) {
        if (originalElement.parentNode === null) {
            throw new Error('Null parent');
        }
        originalElement.parentNode.replaceChild(replacementElement, originalElement);
    }
}

export type ANSWER_CALLBACK = (correct: boolean, showTime: Date) => Promise<void>;