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
      c'8 g,8 d4 |
      e4 d8 e8 |
      a,4 des8 b8 |
      e8 ees8 aes,4 |
      a,4 gis2 |
      g8 g,8 fis4
      \bar "|."
    }
  }
}
