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
    \time 3/4
    \absolute {
      cis'4 b'8 e''8 d'4 |
      d'8 d''8 bes'8 fis''8 g'4 |
      bis'4 aes''8 ges''8 a''8 fis''8 |
      fis''4 d''4 fis''8 fis''8 |
      fis''4 cis'4 cis''4 |
      e''4 cis''8 fis''8 fis''8 ais''8
      \bar "|."
    }
  }
}
