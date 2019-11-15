export interface IQuestion {
    category : string,
    type : string,
    difficulty : string,
    question: string,
    correct_answer : string,
    incorrect_answer : Array<string>;
}