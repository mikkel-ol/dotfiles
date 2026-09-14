# Default setup. scripts/packages composes other profiles from these same files.
# Selection happens before invoking brew: it also works with sanitized environments.
eval File.read(File.join(__dir__, "packages", "Brewfile.core"))
if OS.mac?
  %w[desktop ai].each do |profile|
    eval File.read(File.join(__dir__, "packages", "Brewfile.#{profile}"))
  end
end
