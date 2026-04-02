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
    \key d \major
    \time 4/4
    \absolute {
      bes,4 b4 b8 g8 |
      d2 a2 |
      e4 fis,4 gis,8 a,8 |
      ees4 b,8 fis8 g8 fis,8 |
      fes4 e8 e8 g,4 |
      e,8 fis,8 e8 cis'8 bis,4 |
      b,4 ces'2 fis,4
      \bar "|."
    }
  }
}
