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
            .sortBy(n => n.year)
            .groupBy(n => n.year);
        const currentNotes = this.props.notes.filter(n => n.year === undefined);
        const prevNotes = Immutable.List(notesGroupedAndSortedByYear.keys()).sort().reverse();

        const currentNotesElems =
            <div>
                <h2>current</h2>
                <ul>
                    {currentNotes.map(n => <FinishedStudyItem entry={n} />)}
                </ul>
            </div>;
        const prevNotesElems = prevNotes.map(y => 
            <div>
                <h2>{y}</h2>
                <ul>
                    {notesGroupedAndSortedByYear.get(y)?.map(n => <FinishedStudyItem entry={n} />)}
                </ul>
            </div>);

        return <div>{currentNotesElems}{prevNotesElems}</div>
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
        switch (this.props.entry.source.type) {
            case 'book': {
                return (
                    <li>
                        <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> (book <a href={'https://openlibrary.org/isbn/' + this.props.entry.source.isbn}>ISBN</a>
                        {this.props.entry.source.url === undefined ? null : <span> and <a href={this.props.entry.source.url}>website</a></span>})
                    </li>
                );
            }
            case 'course': {
                return (
                    <li>
                        <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> (course <a href={this.props.entry.source.url}>website</a>)
                    </li>
                );
            }
            case 'document': {
                return (
                    <li>
                        <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> (document <a href={this.props.entry.source.url}>website</a>)
                    </li>
                );
            }
            default:
                throw new Error('This should never happen');
        }

    }
}




export const FinishedStudyEntryV =
    t.readonly(
        t.type({
            year: t.union([
                t.number,
                t.undefined
            ]),
            name: t.string,
            notesUrl: t.string,
            source: t.union([BookV, CourseV, DocumentV])
        })
    );

export type FinishedStudyEntry = t.TypeOf<typeof FinishedStudyEntryV>;