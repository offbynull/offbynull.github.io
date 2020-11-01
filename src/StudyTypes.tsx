import * as t from "io-ts";

export const BookV =
    t.readonly(
        t.type({
            type: t.literal('book'),
            url: t.union([t.string, t.undefined]),
            isbn: t.string
        })
    );

export const CourseV =
    t.readonly(
        t.type({
            type: t.literal('course'),
            url: t.string
        })
    );

export const DocumentV = // generic catchall for online material that isn't a course or a book
    t.readonly(
        t.type({
            type: t.literal('document'),
            url: t.string
        })
    );

export type Book = t.TypeOf<typeof BookV>;
export type Course = t.TypeOf<typeof CourseV>;
export type Document = t.TypeOf<typeof DocumentV>;