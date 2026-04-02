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
    \key g \major
    \time 4/4
    \absolute {
      d'2 e'2 |
      bis'4 ees''4 ges''2 |
      ais''2 a''4 b'4 |
      c''4 d''8 b'8 g'8 e''8 |
      c''4 cis''4 e'4 e''4 |
      eis''8 fes'8 d'4 fis'4 |
      g''4 bes'8 b'8 a'8 e''8
      \bar "|."
    }
  }
}
