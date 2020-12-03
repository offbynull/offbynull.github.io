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
        const currentNotes = this.props.notes.filter(n => n.year === undefined);
        const prevNotesYears = notesGroupedAndSortedByYear.keySeq().sort().reverse();

        const currentNotesElems = <ul>{currentNotes.map(n => <FinishedStudyItem entry={n} />)}</ul>;
        const prevNotesElems = prevNotesYears.map(y => <ul>{notesGroupedAndSortedByYear.get(y)?.map(n => <FinishedStudyItem entry={n} />)}</ul>);
        return (
            <div>
                <ul>
                    {currentNotesElems}{prevNotesElems}
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
        switch (this.props.entry.source.type) {
            case 'book': {
                return (
                    <li>
                        <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> ({year}, book <a href={'https://openlibrary.org/isbn/' + this.props.entry.source.isbn}>ISBN</a>
                        {this.props.entry.source.url === undefined ? null : <span> and <a href={this.props.entry.source.url}>website</a></span>})
                    </li>
                );
            }
            case 'course': {
                return (
                    <li>
                        <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> ({year}, course <a href={this.props.entry.source.url}>website</a>)
                    </li>
                );
            }
            case 'document': {
                return (
                    <li>
                        <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> ({year}, document <a href={this.props.entry.source.url}>website</a>)
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