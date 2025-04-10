import Dexie from 'dexie';

export enum Grade {
    CORRECT_PERFECT = 5,           // correct.
    CORRECT_HESITATION = 4,        // correct -- got it after some hesitation.
    CORRECT_DIFFICULT = 3,         // correct -- got it but it was difficult to think up.
    INCORRECT_REMEMBERED_EASY = 2, // incorrect -- but the correct one was easy to recall.
    INCORRECT_REMEMBERED_HARD = 1, // incorrect -- but the correct one was recalled with difficulty.
    INCORRECT_BLACKOUT = 0         // incorrect -- complete blackout.
}

export interface Question {
    id: number;         // question id
    repetition: number; // how many times the correct answer's been gotten in a row -- initial val is 0.
    interval: number;   // how many days until this question is to be answered again -- initial val is 0.
    eFactor: number;    // easiness factor reflecting how easy memorizing / retaining is -- initial val is 2.5.
    nextUtc: number;    // next time to show this question (as utc) based on the timestamp interval was set -- initial val is 0.
    dead: boolean;      // if set, this question shouldn't be displayed to the user
}

export class AnkiDb {
    private constructor(private readonly db: Dexie) { }

    public static create(name: string): AnkiDb {
        const db = new Dexie('anki_' + name);
        db.version(1).stores({
            questions: 'id, nextUtc, dead'
        });
        return new AnkiDb(db);
    }

    public async trackQuestion(id: number, dead: boolean) {
        const table = this.db.table('questions');
        let question = await table.get(id) as Question;
        if (question === undefined) {
            question = { id: id, repetition: 0, interval: 0, nextUtc: 0, eFactor: 2.5, dead: false};
        }

        if (dead === true) {
            // regardless of if the question already existed in the db or not, if it's been marked as dead reset it, set it
            // to dead, and set the next time it should show to infinity so it never shows up again
            question = { id: id, repetition: 0, interval: 0, nextUtc: Number.POSITIVE_INFINITY, eFactor: 2.5, dead: true};
        } else if (question.dead === true && dead === false) {
            // if the question was dead but it's been resurrected, reset its status as if its brand new
            question = { id: id, repetition: 0, interval: 0, nextUtc: 0, eFactor: 2.5, dead: false};
        }
        await table.put(question);
    }

    public async answerQuestion(id: number, grade: Grade) {
        const table = this.db.table('questions');
        const foundQuestion = (await table.get(id)) as Question;

        // https://super-memory.com/english/ol/sm2.htm
        const correctAnswer = (() => {
            switch (grade) {
                case Grade.CORRECT_DIFFICULT:
                case Grade.CORRECT_HESITATION:
                case Grade.CORRECT_PERFECT:
                    return true;
                case Grade.INCORRECT_REMEMBERED_EASY:
                case Grade.INCORRECT_REMEMBERED_HARD:
                case Grade.INCORRECT_BLACKOUT:
                    return false;
                default:
                    throw Error('This should never happen');
            }
        })();
        if (correctAnswer) {
            switch (foundQuestion.repetition) {
                case 0: {
                    foundQuestion.interval = 1;
                    break;
                }
                case 1: {
                    foundQuestion.interval = 6;
                    break;
                }
                default: {
                    foundQuestion.interval = Math.round(foundQuestion.interval * foundQuestion.eFactor);
                    break;
                }
            }
            foundQuestion.repetition += 1;
        } else {
            foundQuestion.interval = 1;
            foundQuestion.repetition = 0;
        }
        foundQuestion.nextUtc = (() => {
            const date = new Date();
            date.setDate(date.getDate() + 1);
            return date.getTime();
        })();
        foundQuestion.eFactor = Math.max(
            foundQuestion.eFactor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)),
            1.3
        );

        await table.put(foundQuestion);
    }

    public async getQuestion(id: number): Promise<Question | undefined> {
        const table = this.db.table('questions');
        const found = await table.get(id);
        return found as Question | undefined;
    }

    public async deleteQuestion(id: number): Promise<void> {
        const table = this.db.table('questions');
        await table.delete(id);
    }

    public async getNextScheduledQuestion(): Promise<Question | undefined> {
        const table = this.db.table('questions');
        // get the next pending value
        const value = await table
            .orderBy('nextUtc')
            .filter(q => q.dead === false)
            .first() as Question | undefined;
        // if no next pending value, bail out
        if (value === undefined || value.nextUtc >= Date.now()) {
            return undefined;
        }
        // there may be multiple pending values (same nextUtc), so pick one at random to show
        const values = await table
            .where('nextUtc').equals(value.nextUtc)
            .toArray();
        const randomValue = values[Math.floor(Math.random() * values.length)];
        return randomValue;
    }
}