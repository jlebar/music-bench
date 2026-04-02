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
      ces2 e,2 |
      e,4 b4 a,4 dis8 a8 |
      ges,8 d8 d4 e4 e4 |
      ais4 g,4 g4 a,4 |
      bes4 a,4 a,2 |
      ges,8 c'8 fis8 b,8 c4 c4
      \bar "|."
    }
  }
}
