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
      fis4 e8 g8 |
      a4 aes2 |
      ees4 g,2 |
      e,8 bes8 ces8 bes8 bes,4 |
      g,4 c'4 c4 |
      a,4 bes,8 f,8
      \bar "|."
    }
  }
}
