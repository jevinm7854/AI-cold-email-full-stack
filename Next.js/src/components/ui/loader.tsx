// components/ui/loader.tsx
const Loader = () => {
  return (
    <div className="flex justify-center items-center">
      <div className="animate-spin rounded-full border-t-8 border-b-8 border-blue-500 w-24 h-24"></div>
    </div>
  );
};

export default Loader;
