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
    \key c \major
    \time 4/4
    \absolute {
      des8 bes8 g4 dis4 |
      gis8 f,8 a,8 b8 f4 |
      bes,4 g,4 e8 a8 |
      a,4 b,8 c'8 eis,4 |
      aes,4 e4 c'4 e,4
      \bar "|."
    }
  }
}
