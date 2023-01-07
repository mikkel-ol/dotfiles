# 💬 dotfiles

![wow dotfiles](docs/img/dotfiles.meme.png)

# Requirements

- zsh
- rcm

Alternatively you can run the script `bootstrap.sh`. **Note** this installs all my default tools, so make sure you want them all!

# Install

Clone repository into home folder:

```
git clone git@github.com:mikkel-ol/dotfiles.git ~/dotfiles
```

Install the dotfiles:

```
env RCRC=$HOME/dotfiles/rcrc rcup
```

After the initial installation, you can run `rcup` without the one-time variable
`RCRC` being set (`rcup` will symlink the repo's `rcrc` to `~/.rcrc` for future
runs of `rcup`). [See
example](rcrc).

This command will create symlinks for config files in your home directory.
Setting the `RCRC` environment variable tells `rcup` to use standard
configuration options:

- Exclude the `README.md`, `README-ES.md` and `LICENSE` files, which are part of
  the `dotfiles` repository but do not need to be symlinked in.
- Give precedence to personal overrides which by default are placed in
  `~/dotfiles-local`
- Please configure the `rcrc` file if you'd like to make personal
  overrides in a different directory

# Updates

From time to time you should pull down any updates to these dotfiles, and run

```
rcup
```

to link any new files. **Note** You _must_ run
`rcup` after pulling to ensure that all files in plugins are properly installed,
but you can safely run `rcup` multiple times so update early and update often!
