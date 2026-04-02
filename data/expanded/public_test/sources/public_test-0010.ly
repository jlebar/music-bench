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
    \time 3/4
    \absolute {
      c'8 g,8 d8 ces'8 fis4 |
      b4 b,8 d8 fis,8 ais8 |
      d8 ees,8 b4 g4 |
      e8 ees8 aes,8 b,8 e,4 |
      a,4 gis4 g,8 fis8 |
      g4 g,8 fis8 e8 e8
      \bar "|."
    }
  }
}
