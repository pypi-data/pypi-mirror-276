export const tokenTypes = {
    type: 0, // used for types within JSONiq
    namespace: 1, // used for namespaces
    keyword: 2, // used for keywords: for, let, break loop, etc.
    variable: 3, // used for variables
    parameter: 4, // future use for function parameters
    property: 5, // used for object properties
    function: 6, // used for function definition
    comment: 7, // used for comments
    string: 8, // used for string literals
    number: 9, // used for number literals
    operator: 10, // used for operators
    decorator: 11, // used for annotations
    local_storage: 12, // custom type used for local variables
    unknown: 13, // used when no other type can be inferred
    punctuation: 14, // used for brackets, comma and dot.
};
export const tokenModifiers = {
    declaration: 1 << 0, // used for declarations
    static: 1 << 1, // used for static constructs
    definition: 1 << 2, // used for definitions
    readonly: 1 << 3, // used for read-only variables and functions
    defaultLibrary: 1 << 4, // used for built-in library calls
};
export const tokenLegend = {
    tokenTypes: Object.keys(tokenTypes),
    tokenModifiers: Object.keys(tokenModifiers),
};
//# sourceMappingURL=tokenLegend.js.map