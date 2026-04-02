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
      g''4 ees''2 |
      c'4 ees''8 c'8 |
      f''4 ais''4 c''4 |
      a''4 ges'4 ges'4 |
      d'8 ees''8 ais''8 f'8 f''4 |
      f'8 f''8 g'8 d''8 f'4 |
      c'8 d''8 d'8 c'8 ees'4 |
      fes'4 g''4 bes'4
      \bar "|."
    }
  }
}
