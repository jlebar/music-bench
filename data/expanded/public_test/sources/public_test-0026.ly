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
      g'4 g'8 fis''8 |
      d'8 d''8 bes'4 |
      bis'8 aes''8 ges''4 |
      fis''4 d''2 |
      gis''4 cis'8 cis''8 |
      e''8 cis''8 fis''4
      \bar "|."
    }
  }
}
