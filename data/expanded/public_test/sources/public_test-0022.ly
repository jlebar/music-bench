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
      g'4 ges''4 g'8 ces'8 |
      e'2 d''4 g'4 |
      g'4 b'4 fis''2 |
      d'4 g''8 a'8 d''8 d'8 |
      eis'4 fis''8 g'8 a''8 fis'8 |
      cis'4 fis'4 d''4 g''4 |
      e''4 a''4 d'4 b'4 |
      fis'2 g''4 cis''4
      \bar "|."
    }
  }
}
