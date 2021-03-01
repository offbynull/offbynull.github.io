import * as React from "react";
import * as Immutable from "immutable";
import * as t from "io-ts";
import { BookV, CourseV, DocumentV } from "./StudyTypes";



export interface FinishedStudyListProps {
    readonly notes: Immutable.List<FinishedStudyEntry>
};

export interface FinishedStudyListState {
};

export class FinishedStudyList extends React.Component<FinishedStudyListProps, FinishedStudyListState> {
    public constructor(props: FinishedStudyListProps, context?: any) {
        super(props, context);
        this.state = {
        };
    }

    public render() {
        const notesGroupedAndSortedByYear = this.props.notes
            .filter(n => n.year !== undefined)
            .groupBy(n => n.year);
        const wipNotes = this.props.notes.filter(n => n.year === undefined);
        const doneNotesByYear = notesGroupedAndSortedByYear.keySeq().sort().reverse();

        const wipNotesElems = wipNotes.map(n => <FinishedStudyItem entry={n} />);
        const doneNotesElems = doneNotesByYear.map(y => notesGroupedAndSortedByYear.get(y)?.map(n => <FinishedStudyItem entry={n} />));
        return (
            <div>
                <ul>
                    {wipNotesElems}{doneNotesElems}
                </ul>
            </div>
        );
    }
}




export interface FinishedStudyItemProps {
    readonly entry: FinishedStudyEntry
};

export interface FinishedStudyItemState {
};

export class FinishedStudyItem extends React.Component<FinishedStudyItemProps, FinishedStudyItemState> {
    public constructor(props: FinishedStudyItemProps, context?: any) {
        super(props, context);
        this.state = {
        };
    }

    public render() {
        const year = this.props.entry.year || 'WIP';
        return (
            <li>
                <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> ({year})
            </li>
        );
        // switch (this.props.entry.source.type) {
        //     case 'book': {
        //         return (
        //             <li>
        //                 <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a>{/* ({year}, book <a href={'https://openlibrary.org/isbn/' + this.props.entry.source.isbn}>ISBN</a>
        //                 {this.props.entry.source.url === undefined ? null : <span> and <a href={this.props.entry.source.url}>website</a></span>}) */}
        //             </li>
        //         );
        //     }
        //     case 'course': {
        //         return (
        //             <li>
        //                 <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a>{/* ({year}, course <a href={this.props.entry.source.url}>website</a>) */}
        //             </li>
        //         );
        //     }
        //     case 'document': {
        //         return (
        //             <li>
        //                 <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a>{/* ({year}, document <a href={this.props.entry.source.url}>website</a>) */}
        //             </li>
        //         );
        //     }
        //     default:
        //         throw new Error('This should never happen');
        // }
    }
}


const SourceTypeV = t.union([BookV, CourseV, DocumentV]);

export const FinishedStudyEntryV =
    t.readonly(
        t.type({
            year: t.union([
                t.number,
                t.undefined
            ]),
            name: t.string,
            notesUrl: t.string,
            source: t.union([
                SourceTypeV,
                t.readonlyArray(SourceTypeV)
            ])
        })
    );

export type FinishedStudyEntry = t.TypeOf<typeof FinishedStudyEntryV>;