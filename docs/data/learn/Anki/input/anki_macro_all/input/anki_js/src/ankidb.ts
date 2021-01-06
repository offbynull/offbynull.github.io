import Dexie from "dexie";

export class AnkiDb {
    private constructor(private readonly db: Dexie) { }

    public static create(name: string): AnkiDb {
        const db = new Dexie("anki_" + name);
        db.version(1).stores({
            questions: "id, nextUtc"
        });
        return new AnkiDb(db);
    }

    public async trackQuestion(id: number) {
        const table = this.db.table("questions");
        const foundQuestion = await table.get(id) as Question;
        if (foundQuestion === undefined) {
            const newQuestion: Question = { id: id, repetition: 0, interval: 0, nextUtc: 0, eFactor: 2.5};
            await table.add(newQuestion);
        }
    }

    public async answerQuestion(id: number, grade: Grade) {
        const table = this.db.table("questions");
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
                    throw 'This should never happen';
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
        const table = this.db.table("questions");
        const found = await table.get(id);
        return found as Question | undefined;
    }

    public async getNextScheduledQuestion(): Promise<Question | undefined> {
        const table = this.db.table("questions");
        const value = await table
            .orderBy("nextUtc")
            .reverse()
            .first() as Question | undefined;
        if (value !== undefined && value.nextUtc <= Date.now()) {
            return value;
        }
        return undefined;
    }
}

export enum Grade {
    CORRECT_PERFECT = 5,           // correct.
    CORRECT_HESITATION = 4,        // correct -- got it after some hesitation.
    CORRECT_DIFFICULT = 3,         // correct -- got it but it was difficult to think up.
    INCORRECT_REMEMBERED_EASY = 2, // incorrect -- but the correct one was easy to recall.
    INCORRECT_REMEMBERED_HARD = 1, // incorrect -- but the correct one was recalled with difficulty.
    INCORRECT_BLACKOUT = 0         // incorrect -- complete blackout.
}

interface Question {
    id: number;         // question id
    repetition: number; // how many times the correct answer's been gotten in a row -- initial val is 0.
    interval: number;   // how many days until this question is to be answered again -- initial val is 0.
    eFactor: number;    // easiness factor reflecting how easy memorizing / retaining is -- initial val is 2.5.
    nextUtc: number;    // next time to show this question (as utc) based on the timestamp interval was set -- initial val is 0.
}