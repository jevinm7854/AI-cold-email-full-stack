import UrlForm from "./urlForm";
// import UrlFormResponse from "./urlFormResponse";

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
  searchParams: { url?: string };
}) {
  const slug = (await params).slug;
  return (
    <>
      {/* <div>the slug is : {slug}</div> */}
      <div className="flex justify-center text-2xl mt-5">Generate Email:</div>
      <UrlForm slug={slug}  />
    </>
  );
}
