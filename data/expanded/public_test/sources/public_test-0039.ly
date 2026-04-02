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
      ais,4 dis8 aes8 |
      g2 |
      bes2 |
      c8 c'8 c'4 |
      d4 f,4
      \bar "|."
    }
  }
}
