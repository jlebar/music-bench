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
    \time 4/4
    \absolute {
      eis'4 c''4 e''2 |
      ges''4 e'4 a'4 bes'8 c'8 |
      e''4 c''8 d'8 f''4 a'4 |
      c'4 a'4 a''4 e'8 a''8 |
      c''4 ces''2 g'4 |
      fis'4 bes'4 cis''8 g'8 d'4 |
      ais''8 g''8 e''8 f'8 g''4 g''4
      \bar "|."
    }
  }
}
