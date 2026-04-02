\version "2.24.0"

\paper {
  indent = 0\mm
  line-width = 180\mm
  ragged-right = ##t
}

\layout {
  \context {
    \Score
    \override BarNumber.break-visibility = ##(#t #t #t)
    \override BarNumber.self-alignment-X = #CENTER
  }
}

\score {
  \new Staff {
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \clef bass
    \key c \major
    \time 4/4
    \absolute {
      fes,2 d2 |
      eis8 f8 a,4 ais,4 d4 |
      b4 cis'2 f4 |
      aes,2 c2 |
      a8 g8 f4 a4 bis,4 |
      d4 a,8 e,8 f,8 d8 e,4 |
      b2 e,2
      \bar "|."
    }
  }
}
