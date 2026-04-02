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
    \key d \major
    \time 4/4
    \absolute {
      c'2 fis'2 |
      e''8 a''8 cis'4 d''4 |
      cis'4 d'4 bis'4 e'4 |
      b'4 d''4 fis'2 |
      b'4 d''4 b'4 d'4
      \bar "|."
    }
  }
}
