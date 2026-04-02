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
    \time 2/4
    \absolute {
      ges'2 |
      bes'2 |
      f''2 |
      ees''4 a''4 |
      a''4 g''4 |
      gis''4 g''4 |
      c''2
      \bar "|."
    }
  }
}
