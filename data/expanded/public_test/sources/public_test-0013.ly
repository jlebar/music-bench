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
      bes,4 b4 b8 g8 fis4 |
      d2 a2 |
      e4 fis,4 gis,8 a,8 cis'4 |
      ees8 b,8 fis8 g8 fis,4 ees,4 |
      fes4 e8 e8 g,4 b4 |
      e,4 fis,4 e4 cis'8 bis,8 |
      b,4 ces'2 fis,4
      \bar "|."
    }
  }
}
