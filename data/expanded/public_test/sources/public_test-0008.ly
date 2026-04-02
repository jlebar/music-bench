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
    \time 4/4
    \absolute {
      fis,2 c2 |
      g,4 bis,4 f2 |
      c'4 a8 a8 bes,8 c'8 |
      b4 a,4 f,4 cis4 |
      d2 e,2 |
      bes4 a8 e,8 d4 |
      bes2 a,2 |
      g,4 d4 a,2
      \bar "|."
    }
  }
}
