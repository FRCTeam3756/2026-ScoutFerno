import logo from '../assets/logo.webp';

export function Footer() {
  return (
    <footer>
      <div className="mt-8 flex flex-col items-center justify-center p-2 gap-2">
        <div className="h-24 w-96">
          <img src={logo} />
        </div>
      </div>
    </footer>
  );
}
