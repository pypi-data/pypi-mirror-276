import turbodialog


D = turbodialog.TurboDialog()

D.msg("Welcome to\nthe\nDemo!")


x = D.one_of({
    'a1': 'bla',
    'a2': 'blubb di dupp',
})

x = D.index_of(['aa', 'bb', 'cc'])

D.msg(str(x))
