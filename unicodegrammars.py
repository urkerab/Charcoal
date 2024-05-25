from charcoaltoken import CharcoalToken as CT
import re

UnicodeGrammars = {
    CT.Arrow: [
        ["←"], ["↑"], ["→"], ["↓"], ["↖"], ["↗"], ["↘"], ["↙"],
        ["✳", CT.Expression]
    ],
    CT.Multidirectional: [
        [CT.Arrows, CT.Multidirectional],
        ["+", CT.Multidirectional],
        ["X", CT.Multidirectional],
        ["*", CT.Multidirectional],
        ["|", CT.Multidirectional],
        ["-", CT.Multidirectional],
        ["\\", CT.Multidirectional],
        ["/", CT.Multidirectional],
        ["<", CT.Multidirectional],
        [">", CT.Multidirectional],
        ["^", CT.Multidirectional],
        ["K", CT.Multidirectional],
        ["L", CT.Multidirectional],
        ["T", CT.Multidirectional],
        ["V", CT.Multidirectional],
        ["Y", CT.Multidirectional],
        ["7", CT.Multidirectional],
        ["¬", CT.Multidirectional],
        ["⌊", CT.Multidirectional],
        ["⌈", CT.Multidirectional],
        ["⟦", CT.Multidirectional, "⟧"],
        ["⟦", CT.Multidirectional, CT.EOF],
        ["✳✳", CT.Expression],
        [CT.S]
    ],
    CT.Side: [[CT.Arrow, CT.Expression]],
    CT.S: [["¦"], []],
    CT.Span: [
        [CT.Expression, "；", CT.Expression, "；", CT.Expression],
        [CT.Expression, "；", "；", CT.Expression],
        [CT.Expression, "；", CT.Expression],
        [CT.Expression, "；"],
        ["；", CT.Expression, "；", CT.Expression],
        ["；", CT.Expression],
        ["；", "；", CT.Expression],
        ["；", "；"]
    ],

    CT.Arrows: [[CT.Arrow, CT.Arrows], [CT.Arrow]],
    CT.Sides: [[CT.Side, CT.Sides], [CT.Side]],
    CT.Expressions: [[CT.Expression, CT.Expressions], [CT.Expression]],
    CT.WolframExpressions: [
        [CT.WolframExpression, CT.WolframExpressions],
        [CT.WolframExpression]
    ],
    CT.PairExpressions: [
        [CT.Expression, CT.Expression, CT.PairExpressions],
        [CT.Expression, CT.Expression]
    ],
    CT.Cases: [[CT.Expression, CT.Body, CT.Cases], []],

    CT.WolframList: [
        ["⟦", CT.WolframExpressions, "⟧"],
        ["⟦", "⟧"],
        ["⟦", CT.WolframExpressions, CT.EOF],
        ["⟦", CT.EOF]
    ],
    CT.List: [
        ["⟦", CT.Expressions, "⟧"],
        ["⟦", "⟧"],
        ["⟦", CT.Expressions, CT.EOF],
        ["⟦", CT.EOF]
    ],
    CT.Dictionary: [
        ["⦃", CT.PairExpressions, "⦄"],
        ["⦃", "⦄"],
        ["⦃", CT.PairExpressions, CT.EOF],
        ["⦃", CT.EOF]
    ],

    CT.WolframExpression: [[CT.Span, CT.S], [CT.Expression]],
    CT.Expression: [
        [CT.Number, CT.S],
        [CT.String, CT.S],
        [CT.Name, CT.S],
        [CT.List, CT.S],
        ["⟦", CT.Multidirectional, "⟧", CT.S],
        ["⟦", CT.Multidirectional, CT.EOF],
        [CT.Dictionary, CT.S],
        ["«", CT.Program, "»", CT.S],
        ["«", CT.Program, CT.EOF],
        [CT.OtherOperator, CT.S],
        [
            CT.LazyQuarternary, CT.Expression, CT.Expression, CT.Expression,
            CT.Expression, CT.S
        ],
        [
            CT.Quarternary, CT.Expression, CT.Expression, CT.Expression,
            CT.Expression, CT.S
        ],
        [
            CT.LazyTernary, CT.Expression, CT.Expression, CT.Expression,
            CT.S
        ],
        [
            CT.Ternary, CT.Expression, CT.Expression, CT.Expression,
            CT.S
        ],
        [CT.LazyBinary, CT.Expression, CT.Expression, CT.S],
        [CT.Binary, CT.Expression, CT.Expression, CT.S],
        [CT.LazyUnary, CT.Expression, CT.S],
        [CT.Unary, CT.Expression, CT.S],
        [CT.Nilary, CT.S],
        [
            CT.LazyQuarternary, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.S
        ],
        [
            CT.Quarternary, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.S
        ],
        [
            CT.LazyTernary, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.S
        ],
        [
            CT.Ternary, CT.ExpressionOrEOF, CT.ExpressionOrEOF,
            CT.ExpressionOrEOF, CT.S
        ],
        [CT.LazyBinary, CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.S],
        [CT.Binary, CT.ExpressionOrEOF, CT.ExpressionOrEOF, CT.S],
        [CT.LazyUnary, CT.ExpressionOrEOF, CT.S],
        [CT.Unary, CT.ExpressionOrEOF, CT.S]
    ],
    CT.ExpressionOrEOF: [[CT.Expression], [CT.EOF]],
    CT.Nilary: [
        ["Ｓ"], ["Ｎ"], ["Ａ"], ["‽"], ["ＫＡ"], ["ＫＭ"], ["ＫＶ"], ["ＫＫ"],
        ["ⅈ"], ["ⅉ"]
    ],
    CT.Unary: [
        ["±"], ["Ｌ"], ["¬"], ["Ｉ"], ["‽"], ["Ｖ"], ["⊟"], ["↧"], ["↥"], ["⌊"],
        ["⌈"], ["℅"], ["⮌"], ["≕"], ["″"], ["‴"], ["✂"], ["…·"], ["…"], ["～"],
        ["↔"], ["Σ"], ["Π"], ["⊕"], ["⊖"], ["⊗"], ["⊘"], ["ＵＶ"], ["₂"], ["Ｚ"]
    ],
    CT.Binary: [
        ["⁺"], ["⁻"], ["×"], ["÷"], ["∕"], ["﹪"], ["⁼"], ["‹"], ["›"], ["＆"],
        ["｜"], ["…·"], ["…"], ["Ｘ"], ["§"], ["⊞Ｏ"], ["⪫"], ["⪪"], ["⌕Ａ"],
        ["⌕"], ["◧"], ["◨"], ["№"], ["➙"], ["⧴"], ["？"], ["✂"],
        ["↨"], ["⍘"]
    ],
    CT.Ternary: [["✂"]],
    CT.Quarternary: [["✂"]],
    CT.LazyUnary: [],
    CT.LazyBinary: [["∧"], ["∨"]],
    CT.LazyTernary: [["⎇"]],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        ["ＫＤ", CT.Expression, CT.Arrow],
        ["Ｅ", CT.Expression, CT.Expression],
        ["⭆", CT.Expression, CT.Expression],
        ["⊙", CT.Expression, CT.Expression],
        ["⬤", CT.Expression, CT.Expression],
        ["Φ", CT.Expression, CT.Expression],
        ["▷", CT.Expression, CT.WolframList],
        ["▷", CT.Expression, CT.WolframExpression],
        ["▷", CT.Expression]
    ],

    CT.Program: [[CT.Command, CT.S, CT.Program], []],
    CT.NonEmptyProgram: [[CT.Command, CT.S, CT.Program], [CT.Command]],
    CT.Body: [
        ["«", CT.Program, "»"],
        ["«", CT.Program, CT.EOF],
        [CT.Command, CT.S]
    ],
    CT.Command: [
        ["Ｓ", CT.Name],
        ["Ｎ", CT.Name],
        ["Ａ", CT.Name],
        ["Ｖ", CT.Expression],
        [CT.Arrow, CT.Expression],
        [CT.Expression],
        ["Ｐ", CT.Multidirectional, CT.Expression],
        ["Ｐ", CT.Expression],
        ["Ｇ", CT.Sides, CT.Expression],
        ["Ｇ", CT.Multidirectional, CT.Expression, CT.Expression],
        ["ＧＨ", CT.Sides, CT.Expression],
        ["ＧＨ", CT.Multidirectional, CT.Expression, CT.Expression],
        ["ＵＲ", CT.Expression, CT.Expression],
        ["ＵＲ", CT.Expression],
        ["ＵＯ", CT.Expression, CT.Expression, CT.Expression],
        ["ＵＯ", CT.Expression, CT.Expression],
        ["Ｂ", CT.Expression, CT.Expression, CT.Expression],
        ["Ｂ", CT.Expression, CT.Expression],
        [CT.Arrow],
        ["Ｍ", CT.Arrow],
        ["Ｍ", CT.Expression, CT.Arrow],
        ["Ｍ", CT.Expression, CT.Expression],
        ["↶", CT.Expression],
        ["↶"],
        ["↷", CT.Expression],
        ["↷"],
        ["Ｊ", CT.Expression, CT.Expression],
        ["⟲Ｔ", CT.Expression],
        ["⟲Ｔ"],
        ["‖Ｔ", CT.Multidirectional],
        ["‖Ｔ", CT.Arrow],
        ["‖Ｔ"],
        ["⟲Ｐ", CT.Arrow, CT.Number],
        ["⟲Ｐ", CT.Arrow, CT.Expression],
        ["⟲Ｐ", CT.Arrow],
        ["⟲Ｐ", CT.Number],
        ["⟲Ｐ", CT.Expression],
        ["⟲Ｐ"],
        ["‖Ｍ", CT.Multidirectional],
        ["‖Ｍ", CT.Arrow],
        ["‖Ｍ"],
        ["⟲Ｃ", CT.Arrow, CT.Number],
        ["⟲Ｃ", CT.Arrow, CT.Expression],
        ["⟲Ｃ", CT.Arrow],
        ["⟲Ｃ", CT.Number],
        ["⟲Ｃ", CT.Expression],
        ["⟲Ｃ"],
        ["‖Ｃ", CT.Multidirectional],
        ["‖Ｃ", CT.Arrow],
        ["‖Ｃ"],
        ["⟲ＯＯ", CT.Arrow, CT.Number, CT.S, CT.Expression],
        ["⟲ＯＯ", CT.Arrow, CT.Expression, CT.Expression],
        ["⟲ＯＯ", CT.Arrow, CT.Expression],
        ["⟲ＯＯ", CT.Number, CT.S, CT.Expression],
        ["⟲ＯＯ", CT.Expression, CT.Expression],
        ["⟲ＯＯ", CT.Expression],
        ["⟲Ｏ", CT.Arrow, CT.Number],
        ["⟲Ｏ", CT.Arrow, CT.Expression],
        ["⟲Ｏ", CT.Arrow],
        ["⟲Ｏ", CT.Number],
        ["⟲Ｏ", CT.Expression],
        ["⟲Ｏ"],
        ["⟲ＳＯ", CT.Arrow, CT.Number, CT.S, CT.Expression],
        ["⟲ＳＯ", CT.Arrow, CT.Expression, CT.Expression],
        ["⟲ＳＯ", CT.Arrow, CT.Expression],
        ["⟲ＳＯ", CT.Number, CT.S, CT.Expression],
        ["⟲ＳＯ", CT.Expression, CT.Expression],
        ["⟲ＳＯ", CT.Expression],
        ["⟲Ｓ", CT.Arrow, CT.Number],
        ["⟲Ｓ", CT.Arrow, CT.Expression],
        ["⟲Ｓ", CT.Arrow],
        ["⟲Ｓ", CT.Number],
        ["⟲Ｓ", CT.Expression],
        ["⟲Ｓ"],
        ["‖ＯＯ", CT.Multidirectional, CT.Expression],
        ["‖ＯＯ", CT.Arrow, CT.Expression],
        ["‖ＯＯ", CT.Expression],
        ["‖Ｏ", CT.Multidirectional],
        ["‖Ｏ", CT.Arrow],
        ["‖Ｏ"],
        ["‖ＢＯ", CT.Multidirectional, CT.Expression],
        ["‖ＢＯ", CT.Arrow, CT.Expression],
        ["‖ＢＯ", CT.Expression],
        ["‖Ｂ", CT.Multidirectional],
        ["‖Ｂ", CT.Arrow],
        ["‖Ｂ"],
        ["⟲", CT.Expression],
        ["⟲"],
        ["‖", CT.Arrow],
        ["‖"],
        ["Ｃ", CT.Expression, CT.Expression],
        ["Ｆ", CT.Expression, CT.Body],
        ["Ｗ", CT.Expression, CT.Body],
        ["¿", CT.Expression, CT.Body, CT.Body],
        ["¿", CT.Expression, CT.Body],
        ["§≔", CT.Expression, CT.Expression, CT.Expression],
        ["≔", CT.Expression, CT.Name],
        ["≔", CT.Expression, CT.Expression],
        ["¤", CT.Expression],
        ["ＵＢ", CT.Expression],
        ["Ｄ"],
        ["ＲＦ", CT.Expression, CT.Expression, CT.Body],
        ["ＲＷ", CT.Expression, CT.Expression, CT.Body],
        ["Ｒ", CT.Expression],
        ["Ｒ"],
        ["ＵＴ"],
        ["Ｔ", CT.Expression, CT.Expression],
        ["Ｔ", CT.Expression],
        ["⎚"],
        ["ＵＥ", CT.Expression, CT.Expression],
        ["ＵＥ", CT.Expression],
        ["⊞", CT.Expression, CT.Expression],
        ["≡", "«", CT.Expression, CT.Cases, CT.Body, "»"],
        ["≡", "«", CT.Expression, CT.Cases, "»"],
        ["≡", "«", CT.Expression, CT.Cases, CT.Body, CT.EOF],
        ["≡", "«", CT.Expression, CT.Cases, CT.EOF],
        ["≡", CT.Expression, CT.Cases, CT.Body],
        ["≡", CT.Expression, CT.Cases],
        ["ＵＭ", CT.Expression, CT.Expression],
        ["▶", CT.Expression, CT.WolframList],
        ["▶", CT.Expression, CT.WolframExpression],
        ["≦", CT.Binary, CT.Expression, CT.Name],
        ["≦", CT.Unary, CT.Name],
        ["≧", CT.Binary, CT.Expression, CT.Name],
        ["≧", CT.Unary, CT.Name],
        ["ＵＸ", CT.Expression]
    ]
}
