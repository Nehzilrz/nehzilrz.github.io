---
layout:     post
title:      "调整 Terminal.app 的配色"
date:       2015-02-03 11:26:25
author:     平芜泫
category:   码农
tags:
    - "OS X"
    - 配色
    - 配置
---

刚买来 MacBook Air 的时候，会发现它的终端简直挫爆了，白底黑字还没有颜色。然后许多人就会诉诸 iTerm2.app 这样的第三方应用。事实上只要简单配置一下，Terminal.app 也是不错的。

<!--more-->

为了兼容大部分的 Linux 发行版使用习惯，在 ~/.bash_profile 中加入以下内容：

```bash
# Only for Mac OS X, where .bashrc is otherwise ignored
if [ -f ~/.bashrc ]; then
	source ~/.bashrc
fi
if [ -f ~/.bash_aliases ]; then
	. ~/.bash_aliases
fi
```

这几行代码的作用是自动加载 ~/.bashrc 和 ~./bash_aliases 中的配置。其次，创建 ~/.bashrc，加入以下内容：

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# We use colorful bash
export TERM="xterm-color"

# User specific aliases and functions
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
# force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# some more ls aliases
alias ls='ls -G'
alias ll='ls -alF'
alias la='ls -A'

# Set color on grep
alias grep='grep --color=auto'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi


if [ "`id -u`" == "0" ]; then
	PS1='\[\033[01;31m\]\h\[\033[01;34m\] \W \$\[\033[00m\] '
else
	PS1="\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] "
fi

# For schroot environment
if [ -f "/etc/in-chroot" ]; then
  export DISPLAY=:0.0
  if [ "`id -u`" == "0" ]; then
    PS1='\[\033[01;31m\](chroot)\h\[\033[01;34m\] \W \$\[\033[00m\] '
  else
    PS1='\[\033[01;32m\](chroot)\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
  fi
fi

# export the Editor
export EDITOR="vim"
```

代码是从 Debian 系统中直接拷贝出来的，删去了一些和 OS X 没有半点关系的内容。我没有仔细研究 bashrc 的配置，只是这段足够开启彩色模式而已。

此外最后一行 `export EDITOR="vim"` 是我的个人习惯。

最后是解决终端白底黑字的配色问题。个人推荐使用 [Smyck](http://color.smyck.org) 这个配色。安装此配色，然后在 Terminal.app 的配置中设置为默认。如果喜欢磨砂透明，可以调整其背景的透明度和模糊程度。

![Terminal.app Configuration](/upload/2015/02/Terminal.app-colors.png)

最后得到的终端效果为：

![Terminal.app Demo](/upload/2015/02/Terminal.app-demo.png)
