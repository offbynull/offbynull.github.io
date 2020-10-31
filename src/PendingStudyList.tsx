import * as React from "react";
import * as Immutable from "immutable";
import * as t from "io-ts";



export interface PendingStudyListProps {
    readonly notes: Immutable.List<PendingStudyEntry>
};

export interface PendingStudyListState {
};

export class PendingStudyList extends React.Component<PendingStudyListProps, PendingStudyListState> {
    public constructor(props: PendingStudyListProps, context?: any) {
        super(props, context);
        this.state = {
        };
    }

    public render() {
        return (
            <div>
                <ul>
                    {this.props.notes.map(n => <PendingStudyItem entry={n} />)}
                </ul>
            </div>);
    }
}




export interface PendingStudyItemProps {
    readonly entry: PendingStudyEntry
};

export interface PendingStudyItemState {
};

export class PendingStudyItem extends React.Component<PendingStudyItemProps, PendingStudyItemState> {
    public constructor(props: PendingStudyItemProps, context?: any) {
        super(props, context);
        this.state = {
        };
    }

    public render() {
        return (
            <li>
                <a href={this.props.entry.sourceUrl}>{this.props.entry.name}</a>
            </li>
        );
    }
}



export const PendingStudyEntryV =
    t.readonly(
        t.type({
            name: t.string,
            sourceUrl: t.string
        })
    );

export type PendingStudyEntry = t.TypeOf<typeof PendingStudyEntryV>;