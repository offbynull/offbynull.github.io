/**
 * MarkdownNotes
 * Copyright (c) Kasra Faghihi, All rights reserved.
 * 
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 3.0 of the License, or (at your option) any later version.
 * 
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library.
 */

import { RegexScanner, RegexCapture } from "./regex_scanner";

export class Key {
    public constructor(
        public readonly regex: string,
        public readonly flags: string
    ) {}
}

export class Entry {
    public constructor(
        public readonly origKey: Key, // original regex info
        public readonly showPreamble: boolean,
        public readonly showPostamble: boolean,
        public readonly extraData: object) {
    }
}

export interface ScannerEntry {
    scanner: RegexScanner;
    entry: Entry;
}

export interface CaptureEntry {
    capture: RegexCapture;
    entry: Entry;
}

export class RegexScannerCollection {
    private readonly entries: ScannerEntry[] = [];

    public addBookmark(key: Key, showPreamble: boolean, showPostamble: boolean, extraData: object) {
        const entry = new Entry(key, showPreamble, showPostamble, extraData);

        const scanner = RegexScanner.create(key.regex, key.flags);
        this.entries.push({ scanner: scanner, entry: entry });
    }

    public scan(text: string): ScanResult | null {
        const matches: CaptureEntry[] = [];
        for (const entry of this.entries) {
            const match = entry.scanner.scan(text);
            if (match !== null) {
                matches.push({
                    capture: match,
                    entry: entry.entry
                });
            }
        }

        if (matches.length === 0) {
            return null;
        }


        let filterMatches = matches;

        // Sort by earliest matches on the full capture
        filterMatches = filterMatches.slice().sort((a, b) => a.capture.fullIndex < b.capture.fullIndex ? -1 : 1);
        const earliestFullMatchIdx = filterMatches[0].capture.captureIndex;
        filterMatches = filterMatches.filter(m => m.capture.captureIndex === earliestFullMatchIdx);

        // Sort by longest matches on the capture group
        filterMatches = filterMatches.slice().sort((a, b) => a.capture.captureMatch.length > b.capture.captureMatch.length ? -1 : 1);
        const longestCaptureMatchIdx = filterMatches[0].capture.captureMatch.length;
        filterMatches = filterMatches.filter(m => m.capture.captureMatch.length === longestCaptureMatchIdx);

        // Sort by longest matches on full capture
        filterMatches = filterMatches.slice().sort((a, b) => a.capture.fullMatch.length > b.capture.fullMatch.length ? -1 : 1);
        const longestFullMatchIdx = filterMatches[0].capture.fullMatch.length;
        filterMatches = filterMatches.filter(m => m.capture.fullMatch.length === longestFullMatchIdx);

        if (filterMatches.length !== 1) {
            throw new Error('Conflicting bookmark matched:\n' + JSON.stringify(filterMatches, null, 2))
        }
        const finalMatch = filterMatches[0];

        return {
            fullIndex: finalMatch.capture.fullIndex,
            fullMatch: finalMatch.capture.fullMatch,
            captureIndex: finalMatch.capture.captureIndex,
            captureMatch: finalMatch.capture.captureMatch,
            capturePreamble: finalMatch.entry.showPreamble ? finalMatch.capture.capturePreamble : null,
            capturePostamble: finalMatch.entry.showPostamble ? finalMatch.capture.capturePostamble : null,
            key: finalMatch.entry.origKey,
            extraData: finalMatch.entry.extraData
        };
    }

    public viewEntries(): ReadonlyArray<ScannerEntry> {
        return this.entries;
    }
}

export interface ScanResult {
    fullIndex: number,
    fullMatch: string,
    captureIndex: number,
    captureMatch: string,
    capturePreamble: string | null,
    capturePostamble: string | null,
    key: Key,
    extraData: object
}