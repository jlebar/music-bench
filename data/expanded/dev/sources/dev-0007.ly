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
    \key f \major
    \time 3/4
    \absolute {
      g''4 e''4 e''8 g'8 |
      f''4 d'4 d''4 |
      f''2 ais''4 |
      a''2 ges'4 |
      des''2 fes''4 |
      g'8 f'8 g'4 a'4 |
      e''4 bes'4 d'4 |
      fes'2 g''4
      \bar "|."
    }
  }
}
