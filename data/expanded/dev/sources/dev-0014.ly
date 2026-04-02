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
    \key bes \major
    \time 3/4
    \absolute {
      ees8 f,8 eis8 d8 ees4 |
      bis8 bis8 a,8 f8 c'4 |
      ees,4 a,4 bes,4 |
      bes4 a2 |
      f4 bes2 |
      bes,4 c2
      \bar "|."
    }
  }
}
