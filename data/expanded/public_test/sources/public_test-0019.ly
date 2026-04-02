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
      c'4 e'4 d''8 f'8 |
      gis'8 a''8 d''4 a'4 |
      bis'4 e''4 cis'8 c''8 |
      c''2 cis''4
      \bar "|."
    }
  }
}
