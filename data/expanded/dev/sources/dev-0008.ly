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
    \time 2/4
    \absolute {
      b8 b8 fis,4 |
      fis8 c'8 fis4 |
      b,4 des8 fis,8 |
      ges,8 dis8 ges4
      \bar "|."
    }
  }
}
