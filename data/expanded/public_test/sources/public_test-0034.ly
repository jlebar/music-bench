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
    \time 3/4
    \absolute {
      b4 e,4 fis8 e,8 |
      cis'4 e4 eis,8 cis8 |
      a4 a,2 |
      fis,4 fis4 a4
      \bar "|."
    }
  }
}
