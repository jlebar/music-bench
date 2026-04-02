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
      eis8 dis8 bes,8 bes8 c4 |
      a4 aes4 f,8 e,8 |
      ees4 g,8 c8 e,4 |
      eis4 ces4 bes4 |
      g,2 c'4 |
      a,8 f,8 aes4 bis,4
      \bar "|."
    }
  }
}
