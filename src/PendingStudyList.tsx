import * as React from "react";
import * as Immutable from "immutable";
import * as t from "io-ts";
import { BookV, CourseV, DocumentV } from "./StudyTypes";



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
            </div>
        );
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
        switch (this.props.entry.source.type) {
            case 'book': {
                return (
                    <li>
                        <a href={'https://openlibrary.org/isbn/' + this.props.entry.source.isbn}>{this.props.entry.name}</a> (book)
                        {/* {this.props.entry.source.url === undefined ? null : <span> (<a href={this.props.entry.source.url}>website</a>)</span>} */}
                    </li>
                );
            }
            case 'course': {
                return (
                    <li>
                        <a href={this.props.entry.source.url}>{this.props.entry.name}</a> (course)
                    </li>
                );
            }
            case 'document': {
                return (
                    <li>
                        <a href={this.props.entry.source.url}>{this.props.entry.name}</a> (document)
                    </li>
                );
            }
            default:
                throw new Error('This should never happen');
        }
    }
}



export const PendingStudyEntryV =
    t.readonly(
        t.type({
            name: t.string,
            source: t.union([BookV, CourseV, DocumentV])
        })
    );

export type PendingStudyEntry = t.TypeOf<typeof PendingStudyEntryV>;