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
    \clef treble
    \key c \major
    \time 4/4
    \absolute {
      fis'2 d''2 |
      g''4 c'4 e''4 f''4 |
      f''4 g''2 a'4 |
      a'8 g''8 eis''4 ais''4 c''4
      \bar "|."
    }
  }
}
