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
      e,8 g,8 c'4 dis4 |
      c8 g8 fis,8 aes8 bes4 |
      e2 a4 |
      c'8 d8 g8 bes8 f,4
      \bar "|."
    }
  }
}
