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
    \key g \major
    \time 2/4
    \absolute {
      a4 c8 d8 |
      d2 |
      d4 gis8 c'8 |
      c8 e8 d4 |
      ges,8 fis,8 e8 fis,8 |
      ees,8 fis8 a8 a8 |
      b8 bis,8 e,4
      \bar "|."
    }
  }
}
