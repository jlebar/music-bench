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
    \key f \major
    \time 3/4
    \absolute {
      des4 a8 ces8 |
      a,8 eis8 ces'8 bes8 bes4 |
      ais2 bes,4 |
      a,2 a,4 |
      eis,4 fes,2 |
      c4 a,2 |
      g,8 ges,8 f4
      \bar "|."
    }
  }
}
