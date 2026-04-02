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
    \time 2/4
    \absolute {
      bes,4 g,8 a,8 |
      bes,4 a,4 |
      bes,2 |
      bis8 ees8 g8 d8 |
      f,4 ges8 d8
      \bar "|."
    }
  }
}
