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
      e,2 a,4 |
      bes,8 a8 c8 gis,8 fis,4 |
      f,4 f,4 e,8 c8 |
      g,4 g8 eis,8 a8 e,8
      \bar "|."
    }
  }
}
