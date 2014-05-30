(defvar file-clickable-hook nil
  "Mode that creates clickable links in a file, that would help browsing.")

(defvar file-clickable-mode-map nil
  "Keymap for file clickable mode")

(defun jump-to-file()
  (interactive)
  (message "jump to file called")
  (let (p1 p2 myLine strings filename lineno)
  (setq p1 (line-beginning-position) )
  (setq p2 (line-end-position) )
  (setq myLine (buffer-substring-no-properties p1 p2))
  (setq strings (split-string myLine ":" t))
    (pop strings)
    (pop strings)
    (setq filename (pop strings))
    (setq lineno (pop strings))
    (find-file-other-window (file-name-sans-versions filename t))
    (message lineno)
    (goto-line (string-to-number lineno))))



(if file-clickable-mode-map
    nil
  (setq file-clickable-mode-map (make-sparse-keymap))
  (define-key file-clickable-mode-map "\C-x[" 'jump-to-file))


(defun file-clickable()
  "Major mode for malking buffers with certain syntax clickable"
  (interactive)
  (kill-all-local-variables)
  (setq major-mode 'file-clickable)
  (setq mode-name "FileClickEnabler")
  (use-local-map file-clickable-mode-map)
  (run-hooks 'file-clickable-hook))

(provide  'file-clickable)
