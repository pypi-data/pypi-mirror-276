import { documents } from "../../documents.js";
import { TokensParser } from "./tokenIdentification.js";
import { CharStreams } from "antlr4ts";
import { jsoniqLexer } from "../../grammar/jsoniqLexer.js";
import assert from "assert";
const getSemanticTokensFromContent = (content, offset = { line: 0, character: 0 }) => {
    let inputStream = CharStreams.fromString(content);
    let lexer = new jsoniqLexer(inputStream);
    const lexerTokens = lexer.getAllTokens();
    const tokenParser = new TokensParser(lexerTokens);
    const parsedTokens = tokenParser.getSemanticTokens();
    return {
        data: encodeSemanticTokens(parsedTokens, offset),
    };
};
export const semanticTokens = (message) => {
    const params = message.params;
    const content = documents.get(params.textDocument.uri);
    if (!content) {
        return {
            data: [],
        };
    }
    return getSemanticTokensFromContent(content);
};
export const rangeSemanticTokens = (message) => {
    const params = message.params;
    const content = documents.get(params.textDocument.uri);
    if (!content) {
        return {
            data: [],
        };
    }
    const contentLines = content.split(/\r?\n/);
    const startPosition = params.range.start;
    const endPosition = params.range.end;
    let contentForTokens = contentLines[startPosition.line].slice(startPosition.character) + "\n";
    let lineCnt = startPosition.line + 1;
    while (lineCnt < endPosition.line) {
        contentForTokens += contentLines[lineCnt] + "\n";
        ++lineCnt;
    }
    contentForTokens += contentLines[lineCnt].slice(0, endPosition.character);
    return getSemanticTokensFromContent(contentForTokens, startPosition);
};
const encodeSemanticTokens = (tokens, offset) => {
    const result = [];
    const startLine = offset.line;
    let previousPosition = { line: 0, character: 0 };
    for (const token of tokens) {
        let tokenPosition = {
            line: token.startIdx.line + offset.line,
            character: token.startIdx.character,
        };
        // Add offset character to first line tokens.
        if (token.startIdx.line === startLine) {
            tokenPosition.character += offset.character;
        }
        let deltaLine = tokenPosition.line - previousPosition.line;
        // Delta index is relative to previous token in the same line.
        let deltaDiff = previousPosition.line === tokenPosition.line
            ? previousPosition.character
            : 0;
        let deltaIndex = tokenPosition.character - deltaDiff;
        assert(deltaLine >= 0, "Delta line must be positive");
        assert(deltaIndex >= 0, "Delta index must be positive");
        // Now previous becomes current token's start.
        previousPosition = tokenPosition;
        result.push(deltaLine);
        result.push(deltaIndex);
        result.push(token.tokenLength);
        result.push(token.tokenType.typeNumber);
        result.push(token.tokenModifiers.typeNumber);
    }
    return result;
};
//# sourceMappingURL=semanticTokens.js.map