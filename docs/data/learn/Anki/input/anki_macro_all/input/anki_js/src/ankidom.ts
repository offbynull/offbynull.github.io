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

        const patterns = AnkiDom.findAndRemoveClozeWordPatterns(this.processedQuestionTag);
        for (const pattern of patterns) {
            AnkiDom.blackoutClozeWord(this.processedQuestionTag, pattern);
        }
        AnkiDom.addClozeWordAnswerZone(this.processedQuestionTag, patterns, callback);

        this.processedQuestionTag.style.display = 'block';

        AnkiDom.swapElement(
            this.originalQuestionTag,
            this.processedQuestionTag
        );
    }

    private static findAndRemoveClozeWordPatterns(parent: HTMLElement): RegExp[] {
        const nodeIt = document.evaluate(".//guess_word", parent, null, XPathResult.ANY_TYPE, null);
        const ret: RegExp[] = []
        let node = nodeIt.iterateNext();
        while (node !== null) {
            node.parentElement?.removeChild(node);
            if (node.textContent === null) {
                continue;
            }
            const info = (() => {
                const broken = breakOnSlashes(node.textContent);
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
                        throw 'Incorrect number of arguments in guess_word tag: ' + JSON.stringify(broken) + '\n'
                            + '------\n'
                            + 'Examples:\n'
                            + '  `my bookmark`\n'
                            + '  `(my\\s+bookmark)/i`\n'
                            + 'Tag arguments are delimited using forward slash (\). Use \\ to escape the delimiter (\\/).';
                }
            })();
            ret.push(
                    new RegExp(info.regex, info.flags)
            );
            node = nodeIt.iterateNext();
        }
        return ret;
    }

    private static blackoutClozeWord(parent: HTMLElement, pattern: RegExp) {
        function hide(elem: Node) {
            if (elem.nodeName === '#text') {
                const text = (elem as CharacterData).data;
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
                            found[0]
                        )
                    );
                    // hiddenNode.style.visibility = 'hidden;
                    hiddenNode.style.color = 'black';
                    hiddenNode.style.backgroundColor = 'black';
                    hiddenNode.style.userSelect = 'none';
                    containerNode.appendChild(textNode);
                    containerNode.appendChild(hiddenNode);
                    regexLastFoundIdx = regex.lastIndex;
                }
                const finalTextNode = document.createTextNode(
                    text.slice(regexLastFoundIdx)
                );
                containerNode.appendChild(finalTextNode);
                if (elem.parentNode === null) {
                    throw 'Null parent';
                }
                elem.parentNode.replaceChild(containerNode, elem)
            }
            for (let childElem of (elem as Element).children) {
                hide(childElem)
            }
        }
        hide(parent);
    }

    private static addClozeWordAnswerZone(parent: HTMLElement, patterns: RegExp[], callback: ANSWER_CALLBACK) {
        const divElem = document.createElement('div');
        const answerTextElems: HTMLInputElement[] = [];
        for (const pattern of patterns) {
            const answerTextElem = document.createElement('input');
            answerTextElem.setAttribute('type', 'text');
            answerTextElem.setAttribute('id', combineWithSlashes([pattern.source, pattern.flags]));
            divElem.appendChild(answerTextElem);
            divElem.appendChild(
                document.createElement('p')
            );
            answerTextElems.push(answerTextElem);
        }
        const questionShowTime = new Date();
        const submitButtonElem = document.createElement('button');
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
            throw 'Null parent';
        }
        originalElement.parentNode.replaceChild(replacementElement, originalElement);
    }
}

export type ANSWER_CALLBACK = (correct: boolean, showTime: Date) => void;