from charcoaltoken import CharcoalToken as CT
import re

UnicodeGrammars = {
    CT.Arrow: [
        lambda r: [("a", ":Left")],
        lambda r: [("a", ":Up")],
        lambda r: [("a", ":Right")],
        lambda r: [("a", ":Down")],
        lambda r: [("a", ":UpLeft")],
        lambda r: [("a", ":UpRight")],
        lambda r: [("a", ":DownRight")],
        lambda r: [("a", ":DownLeft")],
        lambda r: [("a", ":DownLeft")],
        lambda r: [("$", "Direction"), ("<", "(")] + r[1] + [(">", ")")]
    ],
    CT.Multidirectional: [
        lambda r: r[0] + [(";", ",")] + r[1],
        lambda r: r[0] + [("a", ":Orthogonal"), (";", ",")] + r[1],
        lambda r: r[0] + [("a", ":Diagonal"), (";", ",")] + r[1],
        lambda r: r[0] + [("a", ":All"), (";", ",")] + r[1],
        lambda r: r[0] + [("a", ":Vertical"), (";", ",")] + r[1],
        lambda r: r[0] + [("a", ":Horizontal"), (";", ",")] + r[1]
    ] + [
        (lambda i: lambda r: [("a", ":" + "\\/<>^KTVY7"[i]), (";", ",")] + r[1])(i)
        for i in range(10)
    ] + [
        lambda r: r[0] + [("a", ":DownAndLeft"), (";", ",")] + r[1],
        lambda r: r[0] + [("a", ":UpAndRight"), (";", ",")] + r[1],
        lambda r: r[0] + [("a", ":RightAndDown"), (";", ",")] + r[1],
        lambda r: [("<", "[")] + r[1] + [(">", "]")],
        lambda r: [("<", "[")] + r[1] + [(">", "]")],
        lambda r: [("$", "Directions"), ("<", "(")] + r[1] + [(">", ")")],
        lambda r: []
    ],
    CT.Side: [lambda r: r[0] + r[1]],
    CT.S: [lambda r: [(";", ";")]] * 2,
    CT.Span: [
        lambda r: r[0] + [("$", ";;")] + r[2] + [("$", ";;")] + r[4],
        lambda r: r[0] + [("$", ";;"), ("$", ";;")] + r[3],
        lambda r: r[0] + [("$", ";;")] + r[2],
        lambda r: r[0] + [("$", ";;")],
        lambda r: [("$", ";;")] + r[1] + [("$", ";;")] + r[3],
        lambda r: [("$", ";;")] + r[1],
        lambda r: [("$", ";;"), ("$", ";;")] + r[2],
        lambda r: [("$", ";;"), ("$", ";;")]
    ],

    CT.Arrows: [lambda r: r[0] + [(";", ",")] + r[1], lambda r: r[0]],
    CT.Sides: [lambda r: r[0] + [(";", ",")] + r[1], lambda r: r[0]],
    CT.Expressions: [lambda r: r[0] + [(";", ";")] + r[1], lambda r: r[0]],
    CT.WolframExpressions: [lambda r: r[0] + [(";", ";")] + r[1], lambda r: r[0]],
    CT.PairExpressions: [
        lambda r: r[0] + [(";", ":")] + r[1] + [(";", ",")] + r[2],
        lambda r: r[0] + [(";", ":")] + r[1]
    ],
    CT.Cases: [lambda r: r[0] + [(";", ":")] + r[1], lambda r: []],

    CT.WolframList: [
        lambda r: [("<", "[")] + r[1] + [(">", "]")],
        lambda r: [("<", "["), (">", "]")]
    ] * 2,
    CT.List: [
        lambda r: [("<", "[")] + r[1] + [(">", "]")],
        lambda r: [("<", "["), (">", "]")]
    ] * 2,
    CT.Dictionary: [
        lambda r: [("<", "{")] + r[1] + [(">", "}")],
        lambda r: [("<", "{"), (">", "}")]
    ] * 2,

    CT.WolframExpression: [lambda r: r[0] + r[1], lambda r: r[0]],
    CT.Expression: [
        lambda r: r[0] + r[1]
    ] * 4 + [
        lambda r: [("<", "[")] + r[1] + [(">", "]")] + r[3],
        lambda r: [("<", "[")] + r[1] + [(">", "]")],
        lambda r: r[0] + r[1],
        lambda r: [("<", "{")] + r[1] + [(">", "}")] + r[3],
        lambda r: [("<", "{")] + r[1] + [(">", "}")],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[1] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[1] + r[2] + r[3],
        lambda r: r[0] + r[1] + r[2] + r[3],
        lambda r: r[0] + r[1] + r[2],
        lambda r: r[0] + r[1] + r[2],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1],
        lambda r: r[0],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[1] + r[2] + r[3] + r[4],
        lambda r: r[0] + r[1] + r[2] + r[3],
        lambda r: r[0] + r[1] + r[2] + r[3],
        lambda r: r[0] + r[1] + r[2],
        lambda r: r[0] + r[1] + r[2],
        lambda r: r[0] + r[1],
        lambda r: r[0] + r[1]
    ],
    CT.ExpressionOrEOF: [[CT.Expression], [CT.EOF]],
    CT.Nilary: [
        lambda r: [("o", "InputString")],
        lambda r: [("o", "InputNumber")],
        lambda r: [("o", "Input")],
        lambda r: [("o", "Random")],
        lambda r: [("o", "PeekAll")],
        lambda r: [("o", "PeekMoore")],
        lambda r: [("o", "PeekVonNeumann")],
        lambda r: [("o", "Peek")],
        lambda r: [("o", "i")],
        lambda r: [("o", "j")]
    ],
    CT.Unary: [
        lambda r: [("o", "Negate")],
        lambda r: [("o", "Length")],
        lambda r: [("o", "Not")],
        lambda r: [("o", "Cast")],
        lambda r: [("o", "Random")],
        lambda r: [("o", "Evaluate")],
        lambda r: [("o", "Pop")],
        lambda r: [("o", "Lowercase")],
        lambda r: [("o", "Uppercase")],
        lambda r: [("o", "Floor")],
        lambda r: [("o", "Ceiling")],
        lambda r: [("o", "Character")],
        lambda r: [("o", "Reverse")],
        lambda r: [("o", "GetVariable")],
        lambda r: [("o", "Repeated")],
        lambda r: [("o", "RepeatedNull")],
        lambda r: [("o", "Slice")],
        lambda r: [("o", "InclusiveRange")],
        lambda r: [("o", "Range")],
        lambda r: [("o", "BitwiseNot")],
        lambda r: [("o", "Absolute")],
        lambda r: [("o", "Sum")],
        lambda r: [("o", "Product")],
        lambda r: [("o", "Incremented")],
        lambda r: [("o", "Decremented")],
        lambda r: [("o", "Doubled")],
        lambda r: [("o", "Halved")],
        lambda r: [("o", "PythonEvaluate")],
        lambda r: [("o", "SquareRoot")]
        lambda r: [("o", "Zip")]
    ],
    CT.Binary: [
        lambda r: [("o", "Plus")],
        lambda r: [("o", "Minus")],
        lambda r: [("o", "Times")],
        lambda r: [("o", "Divide")],
        lambda r: [("o", "Modulo")],
        lambda r: [("o", "Equals")],
        lambda r: [("o", "Less")],
        lambda r: [("o", "Greater")],
        lambda r: [("o", "BitwiseAnd")],
        lambda r: [("o", "BitwiseNot")],
        lambda r: [("o", "InclusiveRange")],
        lambda r: [("o", "Range")],
        lambda r: [("o", "Exponentiate")],
        lambda r: [("o", "AtIndex")],
        lambda r: [("o", "PushOperator")],
        lambda r: [("o", "Join")],
        lambda r: [("o", "Split")],
        lambda r: [("o", "FindAll")],
        lambda r: [("o", "Find")],
        lambda r: [("o", "PadLeft")],
        lambda r: [("o", "PadRight")],
        lambda r: [("o", "Count")],
        lambda r: [("o", "Rule")],
        lambda r: [("o", "DelayedRule")],
        lambda r: [("o", "PatternTest")],
        lambda r: [("o", "Slice")],
        lambda r: [("o", "Base")],
        lambda r: [("o", "BaseString")]
    ],
    CT.Ternary: [lambda r: [("o", "Slice")]],
    CT.Quarternary: [lambda r: [("o", "Slice")]],
    CT.LazyUnary: [],
    CT.LazyBinary: [lambda r: [("o", "And")], lambda r: [("o", "Or")]],
    CT.LazyTernary: [lambda r: [("o", "Ternary")]],
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
