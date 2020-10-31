import * as React from "react";
import * as Immutable from "immutable";
import * as t from "io-ts";



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
        const src = (this.props.entry.sourceType === undefined ? 'no source material' : <span>source material <a href={this.props.entry.sourceUrl}>book</a></span>);
        return (
            <li>
                <a href={this.props.entry.notesUrl}>{this.props.entry.name}</a> ({src})
            </li>
        );
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
            sourceUrl: t.string,
            sourceType: t.union([
                t.literal('book'),
                t.literal('course'),
                t.undefined
            ])
        })
    );

export type FinishedStudyEntry = t.TypeOf<typeof FinishedStudyEntryV>;