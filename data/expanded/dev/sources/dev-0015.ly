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
      e8 f,8 eis4 |
      d8 gis,8 bis8 a,8 f4 |
      eis,8 a,8 bes,8 d8 eis4 |
      bes8 fes8 a8 f,8 ees,4 |
      g,4 d8 ces8 |
      bes,2 c4
      \bar "|."
    }
  }
}
